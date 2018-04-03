const State = Object.seal({
    stuff: [],
})

const Api = {
    async getStuff() {
        Object.assign(State, await m.request("/api/stuff/"))
    },
    async postStuff(event) {
        event.preventDefault()
        const data = {hi: event.target.text.value}
        const options = {method: "POST", url: "/api/stuff/", data}
        Object.assign(State, await m.request(options))
    },
}

const Form = {
    view() {
        return m("form", {onsubmit: Api.postStuff},
            m("input", {name: "text", autocomplete: "off"}), m("button", "+"),
        )
    },
}

const Main = {
    oncreate: Api.getStuff,

    view() {
        return m("div",
            State.stuff.map((entry) => m("div", entry)),
            m("div", m(Form)),
        )
    },
}

m.mount(document.body, Main)
