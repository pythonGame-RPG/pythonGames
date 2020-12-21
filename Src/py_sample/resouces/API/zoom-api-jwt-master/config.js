const env = process.env.NODE_ENV || 'production'

//insert your API Key & Secret for each environment, keep this file local and never push it to a public repo for security purposes.
const config = {
	development :{
		APIKey : '',
		APISecret : ''
	},
	production:{	
		APIKey : 'J90bgigZQOeWkliK84T3Jw',
		APISecret : 'k5poD3rkCgLhS8UgrSuAybHREAsQWLJqOnnh'
	}
};

module.exports = config.production
