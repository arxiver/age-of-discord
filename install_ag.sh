wget https://github.com/apache/age/releases/tag/PG13/v1.3.0-
rc0
tar xzf apache-age-1.3.0-src.tar.gz
cd apache-age-1.3.0

echo export AG_PATH=$(pwd) >> ~/.basrch

make PG_CONFIG=$(PG_PATH)/pg_config install
make PG_CONFIG=$(PG_PATH)/pg_config installcheck

psql test
