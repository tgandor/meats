#!/usr/bin/env ruby

ENV['LANG']='C'

IO.popen('df -m .').readlines.each do |line|
    puts line.reverse.gsub(/(\d{3})(?=\d+\s)/, '\1,').reverse
end

