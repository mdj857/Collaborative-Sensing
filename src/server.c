#define _GNU_SOURCE
#include <sys/socket.h>
#include <netinet/in.h>
#include <arpa/inet.h>
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <errno.h>
#include <string.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <fcntl.h>
#include <string.h>
#include <sched.h>
#include <unistd.h>


#define BUFF_SIZE 256
#define STACK_SIZE 2048
#define FALSE 0
#define TRUE 1


int connfd=0;

//thread to read from the fifo and send out the message
int transmit_fifo(void *sparkle){
  int nr;
  char read_buff[BUFF_SIZE];
   int fifo2 = open("srv_transmit", O_RDONLY); //open fifo for reading
   if(fifo2 == -1){
      printf("error opening fifo for reading, %d", errno);
   }
   while(1){
      //read and send to client
      nr = read(fifo2, read_buff, sizeof(read_buff)-1);
      read_buff[nr] = 0; //put termination at end of string
      puts("Transmit FiFo read. Sending to client.");
      write(connfd, read_buff, strlen(read_buff));
 }
  puts("shouldn't go here");
  return(0);
}

int recieve_fifo(void *unused){

  char recvBuff[BUFF_SIZE];
  int fifo3 = open("srv_recieve", O_WRONLY); //open fifo for reading
  if(fifo3 == -1){
    printf("error opening fifo for reading, %d", errno);
  }
  while(1){
    //monitor network and print recieved message to screen
    //TODO: replace print with FiFo write
    int num_char = read(connfd, recvBuff, sizeof(recvBuff));
    recvBuff[num_char] = '\0'; //must add null termination
    puts("Network data recieved. Putting in recieve FiFo");
    write(fifo3, recvBuff, strlen(recvBuff));
    //fputs(recvBuff, stdout);
    //puts(" ");

    if(!strcmp("done\n", recvBuff)){
      //client tells us that we are done so close connexion
      puts("Rarity says the sever is closing down");
      close(connfd); //close the current request
      exit(0); //will this work lol
    }   
  }
  return(0);
}

int main(int argc, char const *argv[]){
  int fifo = 0;
  int fifo2 = 0;
  int listenfd = 0;
  int contin = 1; 
  char user_input[BUFF_SIZE];  //user input string 
  char network_input[BUFF_SIZE];
  struct sockaddr_in serv_addr;
  char *stack, *stack_top,*stack2;
  int done = FALSE;
  int numrv;  
  int num_char=0; 
  char ip_addr[16];

  if(argc != 2){
    puts("Error please specify the IP address of the server!\nE.G. ./server 192.168.56.101");
  }
  
  //process command line arguments
  strncpy(ip_addr, argv[1], 15); //15 is max chars in IPV4 address

  //Transmit FiFo Setup code
  //create fifo, with all permisssions for everyone
  int res = mkfifo("srv_transmit", S_IRUSR | S_IWUSR | S_IRGRP | S_IWGRP | S_IROTH | S_IWOTH);
  if(res && (errno != EEXIST)){ //OK if FiFo already exists
    puts("Error creating the FiFo. Program will now termiate.\n");
    exit(1);
  }
  //open for writing
  fifo = open("srv_transmit", O_RDWR); //open the fifo for reading and writing 
  if(fifo == -1){
    printf("Fifo failed to open, errno %d\n", errno);
    exit(2);
  }

  //Recieve FiFo setup code
  int res2 = mkfifo("srv_recieve", S_IRUSR | S_IWUSR | S_IRGRP | S_IWGRP | S_IROTH | S_IWOTH);
  if(res2 && (errno != EEXIST)){ //OK if FiFo already exists
    puts("Error creating the FiFo. Program will now termiate.\n");
    exit(1);
  }
  //open for writing
  fifo2 = open("srv_recieve", O_RDWR); //open the fifo for reading and writing 
  if(fifo == -1){
    printf("Fifo failed to open, errno %d\n", errno);
    exit(2);
  }

  //server set up code
  listenfd = socket(AF_INET, SOCK_STREAM, 0);
  printf("socket retrieve success\n");
  
  memset(&serv_addr, '0', sizeof(serv_addr));

  serv_addr.sin_family = AF_INET;    
  serv_addr.sin_addr.s_addr = inet_addr(ip_addr);  
  //new-> 192.168.52.101 old-> INADDR_ANY
  serv_addr.sin_port = htons(57681);    
 
  bind(listenfd, (struct sockaddr*)&serv_addr,sizeof(serv_addr));
  
  if(listen(listenfd, 10) == -1){
      printf("Failed to listen\n");
      return -1;
  }
  connfd = accept(listenfd, (struct sockaddr*)NULL ,NULL); // accept awaiting request.
  
  //launch the sending thread
   stack = malloc(STACK_SIZE);
  if(stack == NULL){
     exit(3);;
  }
  stack_top = stack + STACK_SIZE;  /* Assume stack grows toward zero */
  int new_thrd = clone(&transmit_fifo, stack_top,CLONE_THREAD|CLONE_SIGHAND|CLONE_VM, stack);
    if(new_thrd == -1){
    puts("Recieve thread could not be created...Sorry Twilight... :(");
    printf("errno %d\n", errno);
    exit(2);
  }

  //launch the recieving thread  
  stack2 = malloc(STACK_SIZE);
  if(stack2 == NULL){
     exit(3);;
  }
  stack_top = stack2 + STACK_SIZE;  /* Assume stack grows toward zero */
  int nw_thrd2 = clone(&recieve_fifo, stack_top, CLONE_THREAD|CLONE_SIGHAND|CLONE_VM, stack);
    if(nw_thrd2 == -1){
    puts("Thread could not be created...Sorry Twilight... :(");
    printf("errno %d\n", errno);
    exit(2);
  }  
  
  //this code will write into the FIFO
  //TODO replace with infinite loop
  while(contin){ 
     //get user input for message
    //sleep(1);
    // puts("Enter message to send between threads");
    // fgets(user_input, BUFF_SIZE, stdin);
     //put it in the FiFo 
    // write(fifo, user_input, strlen(user_input));
     //rinse and repeat.
     
     //does this work OK 
    // int num_char = read(fifo2, network_input, sizeof(network_input));
    // network_input[num_char] = '\0'; //must add null termination
    // fputs(network_input, stdout);
    // puts(" ");

  }   

  return 0;

}
