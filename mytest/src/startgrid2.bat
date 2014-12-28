D:
java -jar D:\eclipse\workspace\mytest\src\selenium-server-standalone-2.44.0.jar -role node -port 5555 -hub http://localhost:4444/grid/register -browser browserName=firefox,maxInstances=1 -browser browserName=chrome,maxInstances=1 -maxSession 1
