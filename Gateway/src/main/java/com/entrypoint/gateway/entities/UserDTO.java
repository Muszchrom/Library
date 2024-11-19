package com.entrypoint.gateway.entities;

public class UserDTO extends User {
    private String newPassword;

    public String getNewPassword() {
        return this.newPassword;
    }

    public void setNewPassword(String newPassword) {
        this.newPassword = newPassword;
    }
}