wget https://ftp.postgresql.org/pub/source/v13.3/postgresql-13.3.tar.gz

tar xzf postgresql-13.3.tar.gz
cd postgresql-13.3/

mkdir data
chown $(whoami) data

./configure --prefix=$(pwd) --enable-debug
make
make install

export LD_LIBRARY_PATH=$(pwd)/lib
export PATH=$PATH:$(pwd)/bin

echo export PG_PATH=$(pwd) >> ~/.basrch
echo export LD_LIBRARY_PATH=$(pwd)/lib >> ~/.basrch
echo export PATH=$PATH:$(pwd)/bin >> ~/.basrch

# initialize the data directory
./bin/initdb -D ./data

# start the server
./bin/postgres -D ./data >logfile 2>&1 &

# create db named test
./bin/createdb test