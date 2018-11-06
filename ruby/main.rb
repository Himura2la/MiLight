require 'socket'

def all_zones(status = false) return [status ? 0x41 : 0x42, 0x00, 0x55] end

class MiLight
    def initialize(ip)
        myip = Socket::getaddrinfo(Socket.gethostname,"echo",Socket::AF_INET)[-1][3]
        @s = UDPSocket.new
        @s.bind(myip, 52170)
        @s.connect(ip, 8899)
    end

    def set_all(msg)
        @s.send(all_zones().pack("c*"), 0)
        @s.send(msg.pack("c*"), 0)
    end
end

def white() return [0xC2, 0x00, 0x55] end

def brightness(val)
    b = val * (0x18 - 0x02) + 0x02
    return [0x4E, b.round, 0x55]
end

def color(val)
    b = val * 0xFF
    return [0x40, b.round, 0x55]
end

m = MiLight.new('192.168.1.194')

m.set_all(brightness 1)