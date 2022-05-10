//gcc WannaEscape.c -o WannaEscape.exe
//gcc -g WannaEscape.c -o WannaEscape.exe
#include <ctype.h>
#include <stdio.h>
#include <stdlib.h>

int main() {
    FILE* fin = fopen("required_essay.txt", "rb");
    FILE* fout = fopen("required_essay.txt.WannaEscape", "wb");
    if(!fin || !fout) {
		if(fin)
			fclose(fin);
		if(fout)
			fclose(fout);
		return 1;
	}
	
	unsigned char buf[1024];
	size_t bufsz = 0;
	while((bufsz = fread(buf, 1, 1024, fin)) > 0) {
		for(size_t i = 0; i < bufsz; i++) {
			unsigned char c = buf[i];
			c += i % 16 + 0x7f;
			buf[i] = c;
		}
		
		fwrite(buf, 1, bufsz, fout);
	}
	
	fclose(fin);
	fclose(fout);
	system("del required_essay.txt");
	system("del WannaEscape.exe");
    return 0;
}

