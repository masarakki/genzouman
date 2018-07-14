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

1.upto(2) do |page|
  res = client.get('/api/photo/popular.json', limit: 16, p3_photo_list: true, page: page, photo_context: 'popular_feed')
  res.body['list'].each do |x|
    open(x['photo']['sq300_url']) do |f|
      File.write("photos-pop/#{x['photo']['id']}.jpg", f.read)
    end
  end
  sleep 5
end
