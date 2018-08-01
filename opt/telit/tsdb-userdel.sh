#!/bin/bash
sudo su - postgres
echo "Entered as the Postgres user"
psql
echo "Entered PostgreSQL"
echo $1
