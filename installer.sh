export PDOC_ALLOW_EXEC=1
pip uninstall -y pyheaven
chmod -R 777 ./
rm -rf pkg
mkdir pkg
python setup.py bdist_wheel
mv dist/* pkg/
rm -rf __pycache__
rm -rf build
rm -rf dist
pip install --user --find-links=pkg/ --force-reinstall pyheaven
