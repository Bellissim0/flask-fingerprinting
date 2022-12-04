# flask-fingerprinting

The only job of the API server is memorizing the fingerprint to the database, allowing the retrival of saved fingerprints, and change/retrieve the message displayed by the web server

Its endpoinds are:

<strong>POST api/data</strong> it allows to post fingerprints <br />
<strong>GET api/data/<id></strong> it allows to retrieve fingerprint that matches with id <br />
<strong>POST api/hello</strong> it allows you to change the message that website displays <br />
<strong>GET api/hello</strong> it allows you to view the message that website displays <br />
