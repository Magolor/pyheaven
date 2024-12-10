from .cache_utils import *
import openai
import time

DEFAULT_LLM_CONFIG_PATH = pjoin(PYHEAVEN_PATH, "llm_config.json")
def LoadDefaultLLMConfig():
    if not ExistFile(DEFAULT_LLM_CONFIG_PATH):
        CreateFile(DEFAULT_LLM_CONFIG_PATH)
        SaveJson({
            "openai-api": {
                "api_key": None,
                "organization": None,
                "model": "gpt-4o",
                "temperature": 0.0,
                "seed": 42
            }
        }, DEFAULT_LLM_CONFIG_PATH, indent=4)
    return LoadJson(DEFAULT_LLM_CONFIG_PATH)

def LLMInit(path, config=None, clear=True, rm=False,
        openai_api_key=None, openai_api_organization=None,
        aiml_api_key=None, aiml_base_url=None,
        vertex_project_id=None, vertex_location=None, vertex_api_key_refresh_time=None
    ):
    """Initialize the working directory of an LLM instance.
    
    Args:  
        path (str): The LLM path.
        config (dict): The configuration of the LLM instance.
        clear (bool): Whether to clear the LLM directory.
        rm (bool): If True, use `shutil` to enforce remove, otherwise `send2trash` only.
        
        openai_api_key (str): The OpenAI API key. If provided, will overwrite the corresponding value in `config`.
        openai_api_organization (str): The OpenAI API organization. If provided, will overwrite the corresponding value in `config`.
        
        aiml_api_key (str): The AIML API key. If provided, will overwrite the corresponding value in `config`.
        aiml_base_url (str): The AIML API base URL. If provided, will overwrite the corresponding value in `config`.
        
        vertex_project_id (str): The Google Cloud Vertex project ID. If provided, will overwrite the corresponding value in `config`.
        vertex_location (str): The Google Cloud Vertex location. If provided, will overwrite the corresponding value in `config`.
        vertex_api_key_refresh_time (int): The time gap between refreshing the Google Cloud Vertex API key.
    Returns:
        None
    """
    if clear:
        ClearFolder(path, rm=rm)
    if config is None:
        config = LoadDefaultLLMConfig()

    if 'openai-api' not in config:
        config['openai-api'] = {
            "api_key": "<YOUR_OPENAI_API_KEY>",
            "organization": "<YOUR_OPENAI_ORGANIZATION>",
            "model": "gpt-4o",
            "temperature": 0.0,
            "seed": 42
        }
    if openai_api_key is not None:
        config['openai-api']['api_key'] = openai_api_key
    if openai_api_organization is not None:
        config['openai-api']['organization'] = openai_api_organization

    if 'aiml-api' not in config:
        config['aiml-api'] = {
            "api_key": "<YOUR_AIML_API_KEY>",
            "base_url": "https://api.aimlapi.com/v1",
            "temperature": 0.0,
            "seed": 42
        }
    if aiml_api_key is not None:
        config['aiml-api']['api_key'] = aiml_api_key
    if aiml_base_url is not None:
        config['aiml-api']['base_url'] = aiml_base_url
    
    if 'vertex-api' not in config:
        config['vertex-api'] = {
            "project_id": "<YOUR_PROJECT_ID>",
            "location": "us-central1",
            "api_key_refresh_time": 3600,
            "model": "google/gemini-1.5-pro-002",
            "temperature": 0.0,
            "seed": 42
        }
    if vertex_project_id is not None:
        config['vertex-api']['project_id'] = vertex_project_id
    if vertex_location is not None:
        config['vertex-api']['location'] = vertex_location
    if vertex_api_key_refresh_time is not None:
        config['vertex-api']['api_key_refresh_time'] = vertex_api_key_refresh_time
    
    if 'default_backend' not in config:
        config['default_backend'] = "openai-api"
    
    if not ExistFile(pjoin(path, "config.json")):
        SaveJson(config, pjoin(path, "config.json"), indent=4)
    CacheInit(pjoin(path, "cache"), clear=clear, rm=rm)

def LLMSimpleQueryAPI(instance, messages, functions=list(), model=None, temperature=None, seed=None):
    """Query an LLM instance. This is a simple API wrapper for LLM API.
    
    Currently only OpenAI API is supported. You need to set the OpenAI API key and organization before using this function.
    
    Args:
        instance (openai.OpenAI): The LLM instance.
        messages (list): The list of messages to query.
        functions (list): The list of functions to query.
        model (str): The model to be used.
        temperature (float): The temperature to be used.
        seed (int): The seed to be used.
    Returns:
        str: The response of the LLM instance.
    """
    if functions:
        response = instance.chat.completions.create(
            model = model,
            messages = messages,
            functions = functions,
            temperature = temperature,
            seed = seed
        ).choices[0].message
    else:
        response = instance.chat.completions.create(
            model = model,
            messages = messages,
            temperature = temperature,
            seed = seed
        ).choices[0].message
    response = {'role':response.role, 'content':response.content, 'function_call':response.function_call, 'tool_calls':response.tool_calls}
    return response

def LLMQuery(path, messages, functions=list(), backend=None, model=None, temperature=None, seed=None, retry_time=3, retry_gap=0.1):
    """Query an LLM instance. Support config, caching and retrying.
    
    Currently only OpenAI API is supported (aiml and vertex are accessed through `base_url`). You need to set the OpenAI API key and organization before using this function.
    
    Args:
        path (str): The LLM instance path.
        messages (list/str): The list of messages to query. If passed in as a string, it will be converted to a simple message: [{'role':'user', 'content': '<messages>'}].
        functions (list): The list of functions to query.
        model (str): The model to be used.
        temperature (float): The temperature to be used.
        seed (int): The seed to be used.
        retry_time (int): The maximum number of retries. If `retry_time` is 0, the function will be executed only once. If `retry_time` is smaller than 0, the function will be executed indefinitely until it succeeds.
        retry_gap (float): The time gap between retries.
    Returns:
        str: The response of the LLM instance.
    """
    config = LoadJson(pjoin(path, "config.json"))
    if backend is None:
        backend = config["default-api"]
    if backend == "openai-api":
        base_url = None
    elif backend == "aiml-api":
        base_url = config[backend]["base_url"]
    elif backend == "vertex-api":
        base_url = f"https://{config[backend]['location']}-aiplatform.googleapis.com/v1beta1/projects/{config[backend]['project_id']}/locations/{config[backend]['location']}/endpoints/openapi"
        if ('api_key' not in config[backend]) or ('api_key_time' not in config[backend]) or (time.time()-config[backend]['api_key_time'] >= config[backend]['api_key_refresh_time']):
            p = CMD(f"gcloud auth application-default print-access-token", stdout=PIPE)
            api_key, err = p.communicate()
            assert (err is None), f"Failed to get Google Cloud Vertex API key: {err}"
            config[backend]['api_key'] = api_key.decode("utf-8").strip()
            config[backend]['api_key_time'] = int(time.time())
            SaveJson(config, pjoin(path, "config.json"), indent=4)
    else:
        raise NotImplementedError(f"Backend {backend} is not supported.")
    instance = openai.OpenAI(api_key=config[backend]["api_key"], base_url=base_url)
    if model is None: model = config[backend]["model"]
    if temperature is None: temperature = config[backend]["temperature"]
    if seed is None: seed = config[backend]["seed"]
    if isinstance(messages, str): messages = [{'role':'user', 'content': messages}]
    identifier = [model, f"T={(temperature):05.3f}", seed, messages, functions]

    response = CacheGet(pjoin(path, "cache"), identifier, default=None)
    if response is not None:
        return response['content']
    def llm_query():
        response = LLMSimpleQueryAPI(instance, messages, functions, model=model, temperature=temperature, seed=seed)
        CacheSet(pjoin(path, "cache"), identifier, response); return response['content']
    content = Attempt(llm_query, retry_time=retry_time, retry_gap=retry_gap, default=None, verbose=True)
    return content