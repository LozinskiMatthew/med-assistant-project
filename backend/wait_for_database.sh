#!/usr/bin/env bash
# wait_for_database.sh

set -e

host="$1"
port="$2"
shift 2
cmd="$@"

echo "Waiting for $host:$port to be available..."

until nc -z "$host" "$port"; do
  echo "Waiting for $host:$port..."
  sleep 1
done

echo "$host:$port is up!"

exec $cmd
