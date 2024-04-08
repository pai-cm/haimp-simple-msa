# Auth Server

## Tips

### 1. test db 생성하기

````shell
python3 scripts/create_test_db.py ./test.db
````

### 2. 테스트 env 작성
`local.env`에 작성해주시요

````dotenv
DB_HOST='sqlite+aiosqlite:///test.db'
PRIVATE_KEY='-----BEGIN RSA PRIVATE KEY-----
MIICXQIBAAKBgQDH+ifpuRSimi2jFMlZXKQ0qqW/rItLgljGw8W9nK1AekZWjLeU
fYWl2QjQ3MCG7nAtai8sYHU+t7zylv/hKdXU/8bXbpJ1V9GkLmwtuVV3SyYSANdB
PX6gBSXbr9L5hDK2cWYI4CHcMO37XIgXGf8KlM+yjkjb5EFllzC+0Gg+6QIDAQAB
AoGAVFmwlzXhvdpxsI22hnJ8stheFJTXppCDGMgAMwQQ0hchbyVo1AIEKxn6TXsn
3GJbv9Q/tKS1H7DJyrulj9ihIDl7Xfk7+hku8NjrDK9TgQ2S8KSEU7Ilwfdb7Iut
fA1XJADKyLqULXud+XV+LwhoqQ3pmKs9h+lL8JYfhxBm9y8CQQDYuU4KmpEiWCas
GhrG64+QNpH7vI9WJa36uMlXUI9KN8Y69uxfVrL20rkQR8JEWv4/0hwzZoDJDnTy
5YaPLu7bAkEA7DfntLHkDymULkQmRUqKQ+ShbIYv88Vsz0PBcVeGtafuT2cstyCc
DGoMgvn6I2uSXMXZxAGFhttVkKVj3UgKiwJAfVTMeP1iKUZpNuXxzk+zumaUjcxB
6EPqFTB/32rLMtSGYtshXxE4ddzvASc+hWFJ34aWoHMKzzr5Du8FnhA6OQJBALwS
Sr34QH69+QfZJKtYjLs/hjKUqAsrbdWbuaGXMV7ihH/dwqFPKk9MBAgoJTscQ5zv
vdEr8PcNHJQcymT9Hb8CQQCdRJ53abszdnYgPK2pVf0yj1QCztbKRCv0LNuiNVX8
LJKkj4/iYOpWIMzXNgsO3XkHhVzjxGy4kjaV/p9dZpzh
-----END RSA PRIVATE KEY-----'
ACCESS_TOKEN_LIFETIME='86400'
REFRESH_TOKEN_LIFETIME='2592000'
````

### 3. 테스트 시연하기

````shell
python3 -m uvicorn webapp.app:create_app --env-file local.env
````