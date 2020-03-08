del /q dist\*
python setup.py clean --all
python setup.py sdist bdist_wheel
if not %1.==. (
    python setup_forge.py clean --all
    python setup_forge.py sdist bdist_wheel
)
twine check dist\*
if %ERRORLEVEL%==0 (
    twine upload dist\*
)