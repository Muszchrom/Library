package com.entrypoint.gateway.advices;

import org.springframework.http.HttpStatus;
import org.springframework.web.bind.annotation.ExceptionHandler;
import org.springframework.web.bind.annotation.ResponseStatus;
import org.springframework.web.bind.annotation.RestControllerAdvice;

import com.entrypoint.gateway.exceptions.UsernameExistsException;

@RestControllerAdvice
public class UsernameExistsAdvice {
  
  @ExceptionHandler(UsernameExistsException.class)
  @ResponseStatus(HttpStatus.BAD_REQUEST)
  String UsernameExistsHandler(UsernameExistsException ex) {
    return ex.getMessage();
  }
}