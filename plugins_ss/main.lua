io.stderr:write("LUA_DAEMON_READY\n")
io.stderr:flush()

local old_print = print
print = function(...)
    local args = {...}
    for i = 1, #args do
        args[i] = tostring(args[i])
    end
    io.stdout:write("__LOG__ " .. table.concat(args, "\t") .. "\n")
    io.stdout:flush()
end

while true do
    local mode = io.stdin:read("*line")
    if not mode or mode == "__EXIT__" then break end

    local code = io.stdin:read("*line")
    if not code then break end

    if mode == "__EVAL__" then
        local func, err = load("return " .. code)
        if func then
            local ok, result = pcall(func)
            if ok then
                io.stdout:write("__OK__ " .. tostring(result) .. "\n")
            else
                io.stdout:write("__ERR__ " .. tostring(result) .. "\n")
            end
        else
            io.stdout:write("__ERR__ " .. tostring(err) .. "\n")
        end
    elseif mode == "__EXEC__" then
        local func, err = load(code)
        if func then
            local ok, result = pcall(func)
            if ok then
                io.stdout:write("__OK__\n")
            else
                io.stdout:write("__ERR__ " .. tostring(result) .. "\n")
            end
        else
            io.stdout:write("__ERR__ " .. tostring(err) .. "\n")
        end
    end
    io.stdout:flush()
end
