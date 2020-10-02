def isPossible(n,row,col,board):
    #same column
    for i in range(row-1,-1,-1):
       if  board[i][col]==1:
           return False
    # upper left diagonal
    i=row-1
    j=col-1
    while(i>=0 and j>=0):
        if board[i][j]==1:
            return False
        i-=1
        j-=1
    #upper right diagonal
    i=row-1
    j=col+1
    while(i>=0 and j<n): 
        if  board[i][j]==1:
            return False
        i-=1
        j+=1  
    return True        
def nQueenHelper(n,row,board):
    if n==row:
        #we have reached some solution
        # print board matrix and return
        for i in range(0,n):
            for j in range(0,n):
                print( board[i][j],end=" ")
        print()        
        return        
    #place at all possible position and move to smaller problem
    for j in range(0,n):
        if isPossible(n,row,j,board):
            board[row][j]=1
            nQueenHelper(n,row+1,board)
            board[row][j]=0
    return        
def placeQueen(n):
    board = [[0, 0, 0, 0,0, 0, 0, 0,0, 0, 0], 
              [0, 0, 0, 0,0, 0, 0, 0,0, 0, 0], 
              [0, 0, 0, 0,0, 0, 0, 0,0, 0, 0], 
              [0, 0, 0, 0,0, 0, 0, 0,0, 0, 0],[0, 0, 0, 0,0, 0, 0, 0,0, 0, 0], 
              [0, 0, 0, 0,0, 0, 0, 0,0, 0, 0], 
              [0, 0, 0, 0,0, 0, 0, 0,0, 0, 0], 
              [0, 0, 0, 0,0, 0, 0, 0,0, 0, 0],[0, 0, 0, 0,0, 0, 0, 0,0, 0, 0], 
              [0, 0, 0, 0,0, 0, 0, 0,0, 0, 0], 
              [0, 0, 0, 0,0, 0, 0, 0,0, 0, 0], 
              
             ]
    nQueenHelper(n,0,board)
    
n=int(input())
placeQueen(n)

