create user 'user'@'%' identified by '123';

desc mysql.user;

select 
    concat(user, '@', host),
    plugin,
    authentication_string
from mysql.user
where host = '%'
and user = 'user';

grant all privileges 
on *.*
to user@'%';

show grants for user@'%';

select user();