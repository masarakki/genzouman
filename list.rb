#!/usr/bin/env ruby

country_map = {japan: 0, china: 1, brazil: 2}
files = Dir.glob('train/**/*.jpg').map do |x|
  _, c, _ = x.split('/')
  [country_map[c.to_sym], x].join(',')
end

puts files.shuffle.join("\n")
