# PP

## Installation

```bash
pip3 install -r requirements.txt
```

## Usage

- Run the server first
```bash
python3 scripts/ChatServer.py
```

- Run the client in command line
```bash
python3 scripts/ChatClient.py
```

- Run the client in GUI
```bash
cd public/chatroom
python3 -m http.server 9000
```

## WebSocket 数据协议

协议是客户端和服务的通信基础，具体来说是前后端通过 WebSocket 发送的数据解码后的信息体。

协议包含协议版本、事件类型、事件载荷组成。

- 协议版本 `version`：一个版本对应一套协议，未来协议发生破坏性变更时会变更版本号。
- 事件类型 `event`：用于标识本次通信的类型，例如发送消息、撤回消息等等。
- 事件载荷 `data`：用于传递事件类型对应的详细数据。

结构如下：

```tsx
interface WebSocketProtocol {
  version: "1.0",
  event: "message",
  data: [/* 定义为列表, 便于批量传输数据 */]
}
```

### 功能类

#### 下发会话列表

在用户初始化客户端/登录时，由服务端下发该用户拥有的会话列表。

```tsx
interface WebSocketProtocol {
  version: "1.0",
  event: "chatrooms",
  data: [
    {
      room_id: "054692d1-0c09-59d2-89b1-254d9878f0e2",
      room_name: "Peace and love",
      avatar: "/path/to/image.webp",
      members: [
        {
          user_id: "3800d555-50d3-5596-8bcc-d614a9a36601",
          nickname: "Lazy man",
          avatar: "/path/to/image.webp",
        },
        {
          user_id: "4961743b-8ef2-510d-8c93-920a2118abfe",
          nickname: "HOT TEA",
          avatar: "/path/to/image.webp",
        }
      ]
    }
  ]
}
```

### 聊天类

聊天消息类型多种多样，但可抽象为一种固定的结构：

```tsx
interface Message {
  // 发送者
  user_id: "3800d555-50d3-5596-8bcc-d614a9a36601",
  // 会话唯一标识, 不区分群聊和私聊
  room_id: "054692d1-0c09-59d2-89b1-254d9878f0e2",
  // 消息唯一标识
  msg_id: "630eb68f-e0fa-5ecc-887a-7c7a62614681",
  // 消息类型, 可拓展, 未来可支持 text, image, video 等各种类型
  msg_type: "text",
  // 消息内容, 不同消息类型有不同的内容结构数据
  content: {
    text: "test text"
  }
}
```

例如各种 `content` 结构如下：

- 文本消息内容

```tsx
interface MessageContent {
  text: "test text"
}
```

- 图片消息内容

```tsx
interface MessageContent {
  image_uri: "/path/to/image.webp"
}
```

未来可拓展更多的类型，例如表情、富文本、Markdown、音视频通话、加入或退出群聊记录等等。

#### 发送消息（客户端向服务端）

```tsx
interface WebSocketProtocol {
  // 协议版本, 未来结构有破坏性改动时会升级协议版本
  version: "1.0",
  event: "message",
  data: [
    {
      user_id: "3800d555-50d3-5596-8bcc-d614a9a36601",
      room_id: "054692d1-0c09-59d2-89b1-254d9878f0e2",
      msg_id: "630eb68f-e0fa-5ecc-887a-7c7a62614681",
      msg_type: "text",
      content: {
        text: "test text"
      }
    }
  ]
}
```

#### 撤回消息

```tsx
interface WebSocketProtocol {
  // 协议版本, 未来结构有破坏性改动时会升级协议版本
  version: "1.0",
  event: "undo",
  data: [
    {
      user_id: "3800d555-50d3-5596-8bcc-d614a9a36601",
      room_id: "054692d1-0c09-59d2-89b1-254d9878f0e2",
      msg_id: "630eb68f-e0fa-5ecc-887a-7c7a62614681",
    }
  ]
}
```