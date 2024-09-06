class ChatService {
  #address = null
  #socket = null
  #subscribers = []

  constructor(address) {
    this.#address = address
  }

  #createWebSocket(address, onMessage) {
    const socket = new WebSocket(address)

    socket.addEventListener('open', () => {
      console.log('WebSocket connected')
    })

    socket.addEventListener('close', () => {
      console.log('WebSocket closed')
    })

    socket.addEventListener('message', (event) => {
      console.log('WebSocket message received', event.data)
      const data = JSON.parse(event.data)
      onMessage(data)
    })

    return socket
  }

  subscribe(callback) {
    this.#subscribers.push(callback)
  }

  send(message) {
    if (this.#socket == null) {
      throw new Error('WebSocket is not connected')
    }
    this.#socket.send(JSON.stringify(message))
  }

  open() {
    this.#socket = this.#createWebSocket(this.#address, (message) => {
      this.#subscribers.forEach((callback) => {
        callback((message))
      })
    })
  }
}

// create service instance
const service = new ChatService('ws://127.0.0.1:8765/')

// ui & user interaction
const $ = document.querySelector.bind(document)

const contentElement = $('#messages')
const bottomElement = $('#bottom')
const textareaElement = $('#textarea')
const formElement = $('#form')
const loginModalElement = $('#login-modal')
const loginFormElement = $('#login-form')
const loginButtonElement = $('#login-button')

function createMessageAvatarNode(username) {
  const node = document.createElement('div')
  node.classList.add('message-avatar')
  node.innerText = username.substring(0, 1)
  return node
}

function createMessageContentNode(content) {
  const node = document.createElement('div')
  node.classList.add('message-content')
  node.innerText = content
  return node
}

function createMessageTimeNode(timestamp) {
  const node = document.createElement('div')
  node.classList.add('message-time')
  node.innerText = new Date(timestamp).toLocaleString()
  return node
}

function createMessageNode(message) {
  const messageEl = document.createElement('div')
  messageEl.classList.add('message')
  messageEl.dataset.role = message.role

  const avatarEl = createMessageAvatarNode(message.nickname)
  const contentEl = createMessageContentNode(message.content)
  const timeEl = createMessageTimeNode(message.timestamp)

  messageEl.appendChild(avatarEl)
  messageEl.appendChild(contentEl)
  messageEl.appendChild(timeEl)

  return messageEl
}

function addMessage(message) {
  const node = createMessageNode(message)
  contentElement.appendChild(node)
  bottomElement.scrollIntoView({ behavior: 'smooth' })
}

function onKeydown(e) {
  const composing = textareaElement.dataset.composing || 'false'
  if (e.shiftKey == false && e.key === 'Enter' && composing === 'false') {
    e.preventDefault()
    onSubmit()
  }
}

function onCompositionStart() {
  textareaElement.dataset.composing = 'true'
}

function onCompositionEnd() {
  textareaElement.dataset.composing = 'false'
}

function onSubmit() {
  const content = formElement.elements.message.value
  if (content.trim()) {
    const nickname = localStorage.getItem('nickname')
    service.send({
      type: 'message',
      content,
      nickname,
    })
    formElement.reset()
  }
}

textareaElement.addEventListener('keydown', onKeydown)
textareaElement.addEventListener('compositionstart', onCompositionStart)
textareaElement.addEventListener('compositionend', onCompositionEnd)

// user login
function login() {
  return new Promise((resolve) => {
    loginModalElement.showModal()

    loginFormElement.addEventListener('submit', (e) => {
      e.preventDefault()

      const nickname = loginFormElement.elements.nickname.value
      localStorage.setItem('nickname', nickname)
      loginModalElement.close()

      resolve()
    })
  })
}

// check whether user is logged in
if (!localStorage.getItem('nickname')) {
  loginModalElement.showModal()

  login().then(() => {
    service.open()
  })
} else {
  service.open()
}

service.subscribe((message) => {
  const nickname = localStorage.getItem('nickname')
  const role = nickname === message.nickname ? 'user' : 'visitor'
  addMessage({ ...message, role })
})
