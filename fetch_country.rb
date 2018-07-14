#!/usr/bin/env ruby

require 'faraday'
require 'faraday_middleware'
require 'nokogiri'
require 'pry'
require 'open-uri'
require 'fileutils'

client = Faraday.new(url: 'https://worldcosplay.net') do |conn|
  conn.response :json, content_type: /\bjson$/
  # conn.response :logger
  conn.adapter Faraday.default_adapter
end

countries = {japan: [19, 114], brazil: [9, 31], china: [19, 48]}
name = ARGV.pop
countries = countries.reject{|x, y| x != name.to_sym} if name

{ train: 101..500, test: 1..100 }.each  do |type, pages|
  countries.each do |name, area|
    region, country = area
    dirname = "#{type}/#{name}"
    FileUtils.mkdir_p(dirname) unless File.exist?(dirname)

    pages.reverse_each do |page|
      p country: name, page: page
      res = client.get("/api/regions/#{region}/countries/#{country}/photos.json", limit: 16, p3_photo_list: true, page: page)
      res.body['list'].each do |x|
        open(x['photo']['sq300_url']) do |f|
          File.write("#{dirname}/#{x['photo']['id']}.jpg", f.read)
        end
      rescue
        puts x['photo']['sq300_url']
      end
      sleep 10
    end
  end
end
