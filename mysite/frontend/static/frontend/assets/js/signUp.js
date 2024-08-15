var mix = {
	methods: {
		signUp () {
		    const name = document.querySelector('#name').value
			const username = document.querySelector('#login').value
			const phone = document.querySelector('#phone').value
			const email = document.querySelector('#email').value
			const password = document.querySelector('#password').value
			this.postData('/api/sign-up/', JSON.stringify({ name, username, phone, email, password }))
				.then(({ data, status }) => {
					location.assign(`/`)
				})
		}
	},
	mounted() {
	},
	data() {
		return {}
	}
}