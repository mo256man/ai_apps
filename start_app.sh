#!/bin/bash
DIR="$(cd "$(dirname "$0")" && pwd)"

server_cmd="cd \"$DIR/server\" && node index.js; echo 'server'; read"
echo "$server_cmd"
client_cmd="cd \"$DIR/client\" && npm run dev; echo 'client'; read"
echo "$client_cmd"

lxterminal -e bash -ic "bash '$server_cmd'" &
lxterminal -e bash -ic "bash '$client_cmd'" &

# browser wait
url="http://localhost:3001"
until curl -s --head "$URL" >/dev/null 2>&1; do
  sleep 0.5
done

# launch browser
xdg-open "$URL" >/dev/null 2>&1 &

