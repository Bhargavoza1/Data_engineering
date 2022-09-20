#!/bin/sh

mongod localhost:27017/${RSS_NEWS_USER} <<-EOF
    rs.initiate({
        _id: "rs0",
        members: [ { _id: 0, host: getHostName() + ":27017" } ]
    });
EOF
echo "Initiated replica set"

sleep 5

mongod localhost:27017/admin  <<-EOF
    db.createUser({
        user: "admin",
        pwd: "admin",
        roles: [ { role: "userAdminAnyDatabase", db: "admin" } ]
    });
    db.grantRolesToUser("admin", ["clusterManager"]);
EOF

mongod -u admin -p admin localhost:27017/admin <<-EOF
    db.runCommand({
        createRole: "listDatabases",
        privileges: [
            { resource: { cluster : true }, actions: ["listDatabases"]}
        ],
        roles: []
    });
    db.createUser({
        user: "${RSS_NEWS_USER}",
        pwd: "${RSS_NEWS_USER}",
        roles: [
            { role: "readWrite", db: "${RSS_NEWS_USER}" },
            { role: "readWrite", db: "test_${RSS_NEWS_USER}" },
            { role: "read", db: "local" },
            { role: "listDatabases", db: "admin" },
            { role: "read", db: "config" },
            { role: "read", db: "admin" }
        ]
    });
EOF