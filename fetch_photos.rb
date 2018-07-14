#!/usr/bin/env ruby

require 'faraday'
require 'faraday_middleware'
require 'nokogiri'
require 'pry'
require 'open-uri'

client = Faraday.new(url: 'https://worldcosplay.net') do |conn|
  conn.response :json, content_type: /\bjson$/
  conn.adapter Faraday.default_adapter
end

dir = ARGV.pop
unless dir
  puts 'no dir'
  exit 1
end

while line = gets
  begin
    id, url = gets.strip.split(/ +/)
    res = client.get(url)
    image = Nokogiri::HTML(res.body).css('.photo').attr('fullscreenable-url').value
    file = open(image)
    File.write("./#{dir}/#{id}.jpg", file.read)
    sleep 2
  rescue
    true
  end
end
