package com.entrypoint.gateway.entities;

import org.springframework.data.annotation.Id;
import org.springframework.data.relational.core.mapping.Column;
import org.springframework.data.relational.core.mapping.Table;

import com.fasterxml.jackson.annotation.JsonProperty;
import com.fasterxml.jackson.annotation.JsonProperty.Access;
import org.springframework.security.crypto.bcrypt.BCryptPasswordEncoder;

@Table("user_db")
public class User{
    @Column("id") 
    @Id
    private Long id;

    @Column("username")
    private String username;

    @Column("email")
    private String email;

    @Column("phone")
    private Integer phone;

    @Column("role")
    private Integer role;
    
    @JsonProperty(access = Access.WRITE_ONLY)
    @Column("password")
    private String password;

    // , Integer phone,
    public User(String password, String username, String email, Integer phone, Integer role) {
        this.password = password;
        this.username = username;
        this.role = role;
        this.email = email;
        this.phone = phone;
    }

    public String getPassword(){
        return this.password;
    }

    public Long getId() {
        return this.id;
    }

    public String getUsername() {
        return this.username;
    }

    public String getEmail() {
        return this.email;
    }

    public Integer getPhone() {
        return this.phone;
    }

    public Integer getRole(){
        return this.role;
    }

    public void hashPassword() {
        this.password = new BCryptPasswordEncoder().encode(this.password);
    }

    @Override
    public String toString() {
        return "User{" +
            "id=" + this.id + ", " +
            "role="+ this.role + ", " +
            "username=\'" + this.username + "\', " +
            "email=\'" + this.email + "\', " +
            "phone=" + this.phone + ", " +
            "password=\'" + this.password + "\'" +
        "}";
  }
}