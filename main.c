
# include <stdio.h>
# include <string.h>
# include <stdlib.h>
void capturar(char *comando, char *variavel){
    FILE * ponteiro = popen(comando, "r");
    char buffer[100];
    int linha = 1;
	while(fgets(buffer, 100, ponteiro) != NULL){
            if (linha == 2){
                buffer[strcspn(buffer, "\r\n")] = 0;
                strcpy(variavel, buffer);
            }
            linha = linha + 1;
    }
	pclose(ponteiro);
}
int main(int argc, char * argv[]){
	printf(" ==== INFORMAÇÕES DO SISTEMA === \n");

	char os_name[100];
	char cpu[100];
	char arch[100];
	char memory_str[100];


    capturar("wmic os get Caption", os_name);
    capturar("wmic cpu get Name", cpu);
    capturar("wmic os get OSArchitecture",arch);
    capturar("wmic computersystem get TotalPhysicalMemory", memory_str);

    long long bytes = atoll(memory_str);
    long long memory = bytes / (1024 * 1024);

	FILE *arq = fopen("log.txt","w");
    fprintf(arq, "╔════════════════════════════════════════╗\n");
    fprintf(arq, "║          ChickenSC - DIAGNOSTIC        ║\n");
    fprintf(arq, "╚════════════════════════════════════════╝\n\n");
    fprintf(arq, "> System: %s\n> Processor: %s\n> RAM: %lld MB\n> Architecture: %s\n",
                os_name, cpu, memory, arch);
    fprintf(arq, "\n> Note: [AMD64/x86 = Intel/AMD] | [Others = ARM]\n");
    fprintf(arq, "\n══════════════════════════════════════════\n\n");

	fclose(arq);
    system("start notepad.exe log.txt");
}
