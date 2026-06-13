local port = 8888
local server = socket.bind(nil, port)
local client = nil

if server then
    server:listen()
    console:log("CRUD Server listening on " .. port)
else
    console:log("Failed to bind to port " .. port)
end

function tick()
    if not server then return end

    if not client then
        client = server:accept()
        if client then console:log("###New client connected!###") end
    end

    if client then
        local cmd, err = client:receive(1)

        if err == "closed" then
            client:close()
            client = nil
            return
        end

        if cmd == "\1" then -- READ
            local payload = client:receive(3)
            if payload and #payload == 3 then
                local b1, b2, blen = string.byte(payload, 1, 3)
                local addr = b1 * 256 + b2
                local response = ""
                for i = 0, blen - 1 do
                    response = response .. string.char(emu.memory.wram:read8(addr + i))
                end
                client:send(response)
            end

        elseif cmd == "\2" then -- WRITE
            local payload = client:receive(3)
            if payload and #payload == 3 then
                local b1, b2, bval = string.byte(payload, 1, 3)
                local addr = b1 * 256 + b2
                emu.memory.wram:write8(addr, bval)
                client:send("\1")
            end

        elseif cmd == "\3" then -- SOFT RESET / DISCONNECT
            console:log("Received Reset command.")
            console:log("###Closing connection.###")
            client:send("\1") 
            client:close()
            client = nil 

        elseif cmd == "\4" then -- GENERIC BANKED ROM READ
            local payload = client:receive(5)
            if payload and #payload == 5 then
                local bank, a1, a2, l1, l2 = string.byte(payload, 1, 5)
                local local_addr = a1 * 256 + a2
                local len = l1 * 256 + l2
                local flat_address = bank * 0x4000 + (local_addr - 0x4000)
                local response = ""
                for i = 0, len - 1 do
                    response = response .. string.char(emu:read8(flat_address + i))
                end
                client:send(response)
            end

        end
    end
end

callbacks:add("frame", tick)
