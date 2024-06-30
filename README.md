# Transit - Transit Gateway as a Service for OpenStack

# Thiết lập 

Các biến môi trường cần được thiết lập

```
# Database config 

DB_CONNECTION = Kết nối tới cơ sở dữ liệu 

# Vytransit vm config 

VYTRANSIT_FLAVOR_ID = Mã định danh flavor cho máy ảo VyOS
VYTRANSIT_IMAGE_ID = Mã định danh image cho máy ảo VyOS


MANAGEMENT_NETWORK_ID = Mạng quản lý máy ảo VyOS
PEERING_NETWORK_ID = Mạng peering cho Transit Gateway # This is the provider network

VPC_NETWORK_CIDR = Network CIDR cho mạng kết nối giữa VPC và Transit Gateway 

# Transit gateway config 
MAX_VPC_PER_TRANSIT_GATEWAY = Số lượng VPC kết nối với mỗi Transit Gateway
MAX_PEERING_PER_TRANSIT_GATEWAY = Số lượng kết nối Peering với mỗi Transit Gateway 

# Openstack config

Các cài đặt dưới liên quan đến xác thực API cho OpenStack

AUTH_URL=
PROJECT_NAME=
USERNAME=
PASSWORD=
REGION_NAME=
PROJECT_DOMAIN_NAME=
USER_DOMAIN_NAME=

# Celery RabbitMQ config
CELERY_BROKER_URL = Kết nối tới RabbitMQ Broker 

```

# Chạy API Server 
```
python3 -m venv venv 
source venv/bin/activate
cd transit/api 
pip install -e . 
fastapi run 
```

# Chạy worker
```
python3 -m venv venv 
source venv/bin/activate 
cd transit/worker 
pip install -e . 
celery -A celery_worker worker --loglevel=info 
``` 