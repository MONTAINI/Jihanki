#!/usr/bin/ruby
# encoding: utf-8

#ソケット通信
require "socket"

#ポート8090に接続
port = 8090

#クライアント(Android)からの接続を待つソケット
sv = TCPServer.open( port )

#常に繰り返す(無限ループ)
while true do
	#通信接続待ち
        puts "接続待ちだよ"
	#クライアントからの接続を許可する
        sock = sv.accept

	#アクセス先表示 [3]-IP [1]-返信ポート
	puts "#{sock.peeraddr[3]}:#{sock.peeraddr[1]}から接続あり"

        begin
		#クライアントからのデータを受信
                #str1 = "こんにちは"
		str = sock.gets
                puts "受信データ:#{str}"
		#i = File.open("android_test1.txt","w")
		#i.puts(str)

		require "csv"
		str = sock.gets
		i = CSV.open("Person.csv","w") do |user|
		user << ["str"]
		end

		#データ送信はここに書いてね
		f = File.open("jihanki_info.json")
		s = f.read
		sock.write(s )
		f.close
		

		#許可したソケットを閉じる
                sock.close
        rescue
		#通信エラー
                puts "通信エラ＾が発生したよ"
        end
end

#クライアントからの接続を待つソケットを閉じる
#(到達することはない)
sv.close
