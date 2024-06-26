func main() {
	data := []byte("{\n  \"Clients\" : [\n    {\n      \"Hostname\" : \"example.com\",\n      \"IP\" : \"127.0.0.1\",\n      \"MacAddr\" : \"mactonight\"\n    },\n    {\n      \"Hostname\" : \"foo.biz\",\n      \"IP\" : \"0.0.0.0\",\n      \"MacAddr\" : \"12:34:56:78\"\n    }\n  ]\n}")
	var cl ClientInfo
	err := json.Unmarshal(data, &cl)
	if err != nil {
		os.Exit(-1)
	}
}