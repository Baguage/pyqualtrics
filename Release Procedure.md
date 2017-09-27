# Checklist for new release

1. Run unittests for python 2.7 
2. Run unittests for python 3.5
3. Update CHANGELOG.txt
4. Update version in setup.py
5. Push all changes to GitHub
6. Test installation on a different machine in a fresh virtual environment
```bash
cd /tmp
git clone https://github.com/Baguage/pyqualtrics
mkvirtualenv qualtrics
cd pyqualtrics
pip install -r requirements.txt
python setup.py test
python setup.py install
deactivate
rmvirtualenv qualtrics
cd ..
rm -rf pyqualtrics
```

```bash
scl enable rh-python35 bash
cd /tmp
git clone https://github.com/Baguage/pyqualtrics pyqualtrics3
mkvirtualenv qualtrics3
cd pyqualtrics3
pip install -r requirements.txt
python setup.py test
python setup.py install
deactivate
rmvirtualenv qualtrics3
cd ..
rm -rf pyqualtrics3
```

7. Make a release/tag

https://github.com/Baguage/pyqualtrics/releases -> Draft a new release

Use v0.6.2 format for tag name

8. Run `setup.py sdist bdist_egg bdist_wininst upload` command
