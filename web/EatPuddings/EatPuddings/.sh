mysqld start &
service apache2 start &
supervisord -n &
[ -f /.runrunrun ] || {
  sleep 10s
  echo "runrunrun"
  mysqladmin -uroot password 'root' 
  mysql -e "CREATE DATABASE kano DEFAULT CHARACTER SET utf8;" -uroot -proot 
  mysql -e "use kano;source /var/www/html/kano.sql;" -uroot -proot 
  rm /var/www/html/kano.sql 
  chmod -R 655 /var/www/html/
  echo "">/.runrunrun
}
supervisord -n
