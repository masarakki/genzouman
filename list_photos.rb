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

urls = 1.upto(100) do |page|
  res = client.get('/api/photo/popular.json', limit: 16, p3_photo_list: true, page: page, photo_context: 'popular_feed')
  res.body['list'].each do |x|
    puts "#{x['photo']['id']} #{x['photo']['url']}"
  end
end
