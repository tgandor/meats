-- global array, but not in the interpreter...

if #arg == 0 then
    print("No arguments specified.")
    print("Usage: lua[jit] args.lua ARGUMENTS...")
end

for i, val in ipairs(arg) do
    print(i, val)
end