# Checklist for new release

1. Run unittests
2. Update CHANGELOG.txt
3. Update version in setup.py
4. Push all changes to github
5. Test installation on a different machine in a fresh virtual environment
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

6. Make a release/tag

https://github.com/Baguage/pyqualtrics/releases -> Draft a new release

Use v0.6.2 format for tag name

7. Run `setup.py sdist bdist_egg bdist_wininst upload` command
