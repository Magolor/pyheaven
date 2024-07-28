from .cache_utils import *
Import("openai",globals())

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

def LLMInit(path, config=None, clear=True, rm=False, openai_api_key=None, openai_api_organization=None):
    """Initialize the working directory of an LLM instance.
    
    Args:  
        path (str): The LLM path.
        config (dict): The configuration of the LLM instance.
        clear (bool): Whether to clear the LLM directory.
        rm (bool): If True, use `shutil` to enforce remove, otherwise `send2trash` only.
        
        openai_api_key (str): The OpenAI API key. If provided, will overwrite the corresponding value in `config`.
        openai_api_organization (str): The OpenAI API organization. If provided, will overwrite the corresponding value in `config`.
    Returns:
        None
    """
    if clear:
        ClearFolder(path, rm=rm)
    if config is None:
        config = LoadDefaultLLMConfig()
    if 'openai-api' not in config:
        config['openai-api'] = {
            "api_key": None,
            "organization": None,
            "model": "gpt-4o",
            "temperature": 0.0,
            "seed": 42
        }
    if openai_api_key is not None:
        config['openai-api']['api_key'] = openai_api_key
    if openai_api_organization is not None:
        config['openai-api']['organization'] = openai_api_organization
    if not ExistFile(pjoin(path, "config.json")):
        SaveJson(config, pjoin(path, "config.json"), indent=4)
    CacheInit(pjoin(path, "cache"), clear=clear, rm=rm)

def LLMSimpleQueryAPI(messages, functions=list(), backend="openai-api", model=None, temperature=None, seed=None):
    """Query an LLM instance. This is a simple API wrapper for LLM API.
    
    Currently only OpenAI API is supported. You need to set the OpenAI API key and organization before using this function.
    
    Args:
        messages (list): The list of messages to query.
        functions (list): The list of functions to query.
        backend (str): The backend to be used.
        model (str): The model to be used.
        temperature (float): The temperature to be used.
        seed (int): The seed to be used.
    Returns:
        str: The response of the LLM instance.
    """
    
    if backend == "openai-api":
        if functions:
            response = openai.chat.completions.create(
                model = model,
                messages = messages,
                functions = functions,
                temperature = temperature,
                seed = seed
            ).choices[0].message
        else:
            response = openai.chat.completions.create(
                model = model,
                messages = messages,
                temperature = temperature,
                seed = seed
            ).choices[0].message
        response = {'role':response.role, 'content':response.content, 'function_call':response.function_call, 'tool_calls':response.tool_calls}
        return response
    else:
        raise NotImplementedError(f"Backend {backend} is not supported.")

def LLMQuery(path, messages, functions=list(), backend="openai-api", model=None, temperature=None, seed=None, retry_time=3, retry_gap=0.1):
    """Query an LLM instance.
    
    Currently only OpenAI API is supported.
    
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
    if backend == "openai-api":
        openai.api_key = config[backend]["api_key"]
        openai.organization = config[backend]["organization"]
    else:
        raise NotImplementedError(f"Backend {backend} is not supported.")
    if model is None: model = config[backend]["model"]
    if temperature is None: temperature = config[backend]["temperature"]
    if seed is None: seed = config[backend]["seed"]
    if isinstance(messages, str): messages = [{'role':'user', 'content': messages}]
    identifier = [model, f"T={(temperature):05.3f}", seed, messages, functions]

    response = CacheGet(pjoin(path, "cache"), identifier, default=None)
    if response is not None:
        return response['content']
    def llm_query():
        response = LLMSimpleQueryAPI(messages, functions, model=model, temperature=temperature, seed=seed)
        CacheSet(pjoin(path, "cache"), identifier, response); return response['content']
    content = Attempt(llm_query, retry_time=retry_time, retry_gap=retry_gap, default=None, verbose=True)
    return content