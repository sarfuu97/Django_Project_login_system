echo "BUILD START"
python 3.10.8 -m pip install -r requirements.txt
python 3.10.8 manage.py collectstatic --noinput --clear
echo "BUILD END"