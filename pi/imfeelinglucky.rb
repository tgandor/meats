#!/usr/bin/ruby

require 'yt_util'

puts "Querying..."
results = YtUtil::Scrape.query(ARGV.join(" "))
results = results.map {|i| i[:video] }.compact
puts "Results are in."

# Some results may not play so we need to verify a URL returns
#results.shuffle.each do |code| # Iterate over results for a valid video
results.each do |code| # Iterate over results for a valid video
  puts "Attempting video extraction."
  puts code
  urls = `youtube-dl -F #{code}`
  format = nil
  urls.each_line { |line|
    if line =~ /only/
      next
    end
    if line =~ /best/ && line =~ /mp4/
      puts line
      format = line.split()[0]
      break
    end
  }
  if not format
    puts 'No suitable format found'
    next
  end
  command = "omxplayer -o local `youtube-dl -f #{format} -g #{code}`"
  puts command
  if system(command)
    break
  end
end
puts "Extraction successful!"
