export AUTH0_DOMAIN='still-butterfly-7094.us.auth0.com'
export ALGORITHMS='RS256'
export API_AUDIENCE='udacityfinal'

#heroku database url
export DATABASE_URL='postgres://ulxxdhwkddjwqy:85e70942145391f2ffdb063db6bcc4e425659cdef7682654893e88d2a2c945c2@ec2-18-209-78-11.compute-1.amazonaws.com:5432/d3u8jvplibk40e'

#JWTS for all the 3 roles/users: Latest with 24 hours expiration
#Landlord
export ASSISTANT_TOKEN='eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6ImpYTDlESW1zYmRyWmlmQWtCNms1MyJ9.eyJpc3MiOiJodHRwczovL3N0aWxsLWJ1dHRlcmZseS03MDk0LnVzLmF1dGgwLmNvbS8iLCJzdWIiOiJhdXRoMHw2MzUwMTI4YTlhZTk1ZDc0YTM3NGQ0ZTQiLCJhdWQiOiJ1ZGFjaXR5ZmluYWwiLCJpYXQiOjE2NjYzNTgyNjYsImV4cCI6MTY2NjM2NTQ2NiwiYXpwIjoiTUFiZXIzcnBhRHZJR2tBdFRQOHBRVmQ1dHRtUjB4T3MiLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbXX0.vAdB2VGYFZRKhChyeWYJ5fGqC5BUgcQTjd2g54F15bk-m-Nl0Vd7Y-zXFfmry-RVJd4mj1qIue0h5IxwRcWgEAnguRZ_20vUDJmCVZmeT8XzsourYr4zVGH5h8Rq9xiEzyqKjudIDQIUGnU4cUTfsRx9sto_MujltR7_LtEBwGJPCTQRrpYb9MtVrzyE2PJARAuM_gukrtLYExAW3qP6NmRvn0mlMxnANgXBlPf88-UbomGEFNJ8BZjSD8frUieo06MO1cZzjuHcUMqupTQfeh8H4Aj-fx3Dx3YgRG0oxIHOj4ekCfPx-zssW83d0uoxVP-r4UdwT3Z0uPEFSGTtdg'
#Tenant
export DIRECTOR_TOKEN='eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6ImpYTDlESW1zYmRyWmlmQWtCNms1MyJ9.eyJpc3MiOiJodHRwczovL3N0aWxsLWJ1dHRlcmZseS03MDk0LnVzLmF1dGgwLmNvbS8iLCJzdWIiOiJhdXRoMHw2MzUwMTJhZWExMjc1MmZmNDhmZDJkZTciLCJhdWQiOiJ1ZGFjaXR5ZmluYWwiLCJpYXQiOjE2NjYzNTg0MDUsImV4cCI6MTY2NjM2NTYwNSwiYXpwIjoiTUFiZXIzcnBhRHZJR2tBdFRQOHBRVmQ1dHRtUjB4T3MiLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbXX0.PJeN5hH6gdSYsWCYHfIE3bSTsUppPCvYRgwBni2bY4QuHgTzuMnH22iXE96ZEX5prJUoiiWYiqIe57MOla2TG-mtwxzctv2VxvErGmRHV6XHJ01PwcpdI0lc7n3EJ5shEuJobjU72TBEnuFT3hgOe3eeCLLuOTv8mMx8rgmOQMbdyhT1Xcco0LSgH-2hkhMATYbYeZOSwbOG2NGrBtUXz4NXO3QNDekRArjQufhZdbGl3i-TnySAAMu1dAokt-f627EGxg6JvtJyOeKUbXt6vNKqjn_YLSyT9WrsLkcvtczV8VS6zaaV6AMjIN3NB9EITsvLHKZ0oE17t3uVUlBLrA'
#Roommate
export PRODUCER_TOKEN='eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6ImpYTDlESW1zYmRyWmlmQWtCNms1MyJ9.eyJpc3MiOiJodHRwczovL3N0aWxsLWJ1dHRlcmZseS03MDk0LnVzLmF1dGgwLmNvbS8iLCJzdWIiOiJhdXRoMHw2MzUwMTJjZDlhZTk1ZDc0YTM3NGQ0ZTciLCJhdWQiOiJ1ZGFjaXR5ZmluYWwiLCJpYXQiOjE2NjYzNTg1MzksImV4cCI6MTY2NjM2NTczOSwiYXpwIjoiTUFiZXIzcnBhRHZJR2tBdFRQOHBRVmQ1dHRtUjB4T3MiLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbXX0.UVW2ySBneROsBj1Ub2m1OYPSLiBozBzKKpwS-A6-z9PUyzZih69aPZ1cZI8ftsehttHgMS-mej8h8Vh48v9Kp0njhOVJIq5VhXCy1bYS0jMKTlCtzK4BrQ0q49IeFIMpBZCaiFJHJQlyfgscFtNlTLPXNztHRdNbAco2W-8fYdaoBaTgVzLQXj8cQfS8w6bXg-iJew93__yFmCoG9TLGnfuBgLPa9z4YmveY7Lcwm2x6IR_Fa2c7qjy1m5CJ9E0Aoo34c878hyrvd8feVYQaYrAA-CLMvPu6Bx4YkxqVujO5DimvJGRmAbQc8OjfqF0TK1-6pQ6gOeHopE6ZRXo_bQ'