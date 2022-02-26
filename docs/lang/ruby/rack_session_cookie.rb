require 'base64'
require 'cgi'

# 'SessionId' class possibly not provided by import.
# A dummy definition is needed for the Marshal.load()
#require 'rack'
class Rack::Session::SessionId
end

cookie = "....."

obj = Marshal.load(Base64.decode64(CGI.unescape(cookie.split("\n").join).split('--').first))
