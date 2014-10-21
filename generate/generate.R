#!/usr/bin/env Rscript

df.impulse = function(df) {
  df$x=df$x+df$u/10.0
  df$y=df$y+df$v/10.0
  df$z=df$z+df$w/10.0
  df$u=df$u+rnorm(100)/10.0
  df$v=df$v+rnorm(100)/10.0
  df$w=df$w+rnorm(100)/10.0
  df$val=df$val+runif(100)/10-0.05
  df$burn=as.numeric(xor(df$burn,round(runif(100)*0.8)))

  return(df)
}


df=data.frame(x=rnorm(100),y=rnorm(100),z=rnorm(100),
              u=rnorm(100),v=rnorm(100),w=rnorm(100),
              burn=round(runif(100)), val=runif(100))

for(i in seq(0, 100)) {
   df=df.impulse(df)
   fname=sprintf("points.%04d.csv",i)
   write.csv(df,fname,row.names=F,quote=F)
}


