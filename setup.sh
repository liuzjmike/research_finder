user=`whoami`
dbpasswd=dbpasswd

bash db-research/setup.sh
pip install flask Flask-WTF Flask-SQLAlchemy
sed -i "s/vagrant/$user/g;s/dbpasswd/$dbpasswd/g" config.py