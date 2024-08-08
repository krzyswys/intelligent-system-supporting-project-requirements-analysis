package models

type User struct {
	ID           int    `json:"id"`
	Username     string `json:"username"`
	Email        string `json:"email"`
	Password     string `json:"-"`
	Token        string `json:"token"`
	RefreshToken string `json:"refresh_token"`
	Friends      []int  `json:"friends"`
	Projects     []int  `json:"projects"`
	AvatarURL    string `json:"avatar_url"`
}
