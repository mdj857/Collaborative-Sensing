#define _GNU_SOURCE
#include <stdio.h>
#include <stdlib.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <fcntl.h>
#include <string.h>
#include <sched.h>
#include <unistd.h>
#include <errno.h>

#define BUFF_SIZE 128
#define STACK_SIZE 1048
#define FALSE 0
#define TRUE 1

static char read_buff[BUFF_SIZE];
int fifo;
int nr=0;

int read_fifo(void *unused){
   int fifo2 = open("test_fifo", O_RDONLY); //open fifo for reading
   if(fifo2 == -1){
      printf("error opening fifo for reading, %d", errno);
   }
   while(1){
      //read and print to the screen
      nr = read(fifo2, read_buff, sizeof(read_buff)-1);
      read_buff[nr] = 0; //put termination at end of string
      //sleep(2); //just to slow it down so it doesn't come it at once
      puts("Read thread has run Twi. Message is:");
      puts(read_buff);
 }
  puts("shouldn't go here");
   return(0);
}


//main thread of the program...
int main(void){
  char user_input[BUFF_SIZE];  //user input string 
  char *stack, *stack_top;
  int done = FALSE;

  //create fifo
  int res = mkfifo("test_fifo", S_IRUSR | S_IWUSR | S_IRGRP | S_IWGRP | S_IROTH | S_IWOTH);  //everyone gets all the permissions
  if(res){
     if(errno != EEXIST ){
        puts("Error creating the FiFo. Program will now termiate.\n");
        exit(1);
     }    
  }
  //open for writing
  fifo = open("test_fifo", O_RDWR); //open the fifo for reading  
  if(fifo == -1){
     printf("Fifo failed to open, errno %d\n", errno);
  }
  //create a new thread for reading 
  stack = malloc(STACK_SIZE);
  if(stack == NULL){
     exit(3);;
  }
  stack_top = stack + STACK_SIZE;  /* Assume stack grows toward zero */
  int new_thread = clone(&read_fifo, stack_top, CLONE_THREAD | CLONE_SIGHAND | CLONE_VM , stack);
    if(new_thread == -1){
    puts("Thread could not be created...Sorry Twilight... :(");
    printf("errno %d\n", errno);
    exit(2);
  }
  while(!done){
     //get user input for message
     sleep(1); 
     puts("Enter message to send between threads");
     fgets(user_input, BUFF_SIZE, stdin);
     if(!strcmp(user_input, "done\n")){
        puts("Terminating Execution");
        //kill the other thread and exit
	exit(0);
     }
     //put it in the FiFo 
     write(fifo, user_input, strlen(user_input));
     //rinse and repeat.
  } 


  return(0);
}



