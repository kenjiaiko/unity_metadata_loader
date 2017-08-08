import idaapi
import sys
import os
import re

def err(s):
	print s
	sys.exit()

def IncreaseAddr(addr):
	return addr + 4

def DecreaseAddr(addr):
	return addr - 4

def GetVarFromAddr(addr, arch, bits, method=True):
	if arch == "arm":
		if bits == 32:
			if method == True:
				return idc.Dword(addr) & 0xFFFFFFFFFE
			else:
				return idc.Dword(addr)
		else:
			return idc.Qword(addr)
	if arch == "x86":
		if bits == 32:
			return idc.Dword(addr)
		else:
			return idc.Qword(addr)
	err("Error: unsupported arch")

def LoadMethods(ea, method_name):
	fh = open(method_name)
	str_count = fh.readline();
	for line in fh:
		line = line.strip(' ').replace('\r', '').replace('\n', '')
		new_line = re.sub(r'[^a-zA-Z0-9_$]', '_', line)
		addr = GetVarFromAddr(ea, "arm", 32)
		ret = idc.MakeNameEx(addr, str(new_line), SN_NOWARN)
		i = 0;
		while ret == 0:
			new_line_rand = new_line + '_' + str(i)
			ret = idc.MakeNameEx(addr, str(new_line_rand), SN_NOWARN)
			idc.MakeComm(ea, str(line))
			i = i + 1
			if 10 < i:
				break
		ea = IncreaseAddr(ea)
	fh.close()

def LoadStrings(ea, string_literal):
	fh = open(string_literal)
	str_count = fh.readline();
	for line in fh:
		line = line.strip(' ').replace('\r', '').replace('\n', '')
		new_line = 'StringLiteral_' + re.sub(r'[^a-zA-Z0-9_$]', '_', line)
		addr = GetVarFromAddr(ea, "arm", 32, False)
		ret = idc.MakeNameEx(addr, str(new_line), SN_NOWARN)
		i = 0;
		while ret == 0:
			new_line_rand = new_line + '_' + str(i)
			ret = idc.MakeNameEx(addr, str(new_line_rand), SN_NOWARN)
			idc.MakeComm(ea, str(line))
			i = i + 1
			if 10 < i:
				break
		ea = DecreaseAddr(ea)
	fh.close()

def SearchBaseAddress(sz):
	seg = idc.FirstSeg()
	while seg != idc.BADADDR:
		if idc.SegName(seg) == ".data.rel.ro":
			break
		seg = idc.NextSeg(seg)
	while idc.SegName(seg) == ".data.rel.ro":
		if idc.Dword(seg) == sz:
			func = idc.Dword(idc.Dword(seg + 4))
			# MOV R0, R1
			# BX LR
			if idc.Dword(func + 0x00) == 0xE1A00001 and idc.Dword(func + 0x04) == 0xE12FFF1E:
				break
		seg += 4
	if idc.SegName(seg) != ".data.rel.ro":
		err("Error: I couldn't search BaseAddress")
	strct = seg
	offset_of_method_start = idc.Dword(strct + 0x04)
	offset_of_string_start = idc.Dword(strct + 0x74)
	p = offset_of_string_start
	while (idc.Dword(p) + 4) == idc.Dword(p + 4):
		p += 4
	offset_of_string_finish = p
	return (offset_of_method_start, offset_of_string_finish)

def main():
	path = os.getcwd()
	method_name = "./method_name.txt"
	if os.path.isfile(method_name) == False:
		err("Error: method_name.txt not found, execute 'unity_decoder.exe' before loading this script.")
	string_literal = "./string_literal.txt"
	if os.path.isfile(string_literal) == False:
		err("Error: string_literal.txt not found, execute 'unity_decoder.exe' before loading this script.")
	(offset_of_method_start, offset_of_string_finish) = SearchBaseAddress(
		int(open(method_name).readline().rstrip()))
	print "offset of method start: " + str(hex(offset_of_method_start))
	LoadMethods(offset_of_method_start, method_name)
	print "offset of string finish: " + str(hex(offset_of_string_finish))
	LoadStrings(offset_of_string_finish, string_literal)

main()
