const socket = io();
const room = "abc123";  // Tạm thời sử dụng một phòng cố định

socket.emit("join", { room });

let peerConnection;
const config = {
    iceServers: [{ urls: "stun:stun.l.google.com:19302" }]
};

const localVideo = document.getElementById("localVideo");
const remoteVideo = document.getElementById("remoteVideo");

navigator.mediaDevices.getUserMedia({ video: true, audio: true })
    .then(stream => {
        localVideo.srcObject = stream;

        peerConnection = new RTCPeerConnection(config);
        stream.getTracks().forEach(track => peerConnection.addTrack(track, stream));

        peerConnection.ontrack = event => {
            remoteVideo.srcObject = event.streams[0];
        };

        peerConnection.onicecandidate = event => {
            if (event.candidate) {
                socket.emit("signal", { room, candidate: event.candidate });
            }
        };

        socket.on("signal", async ({ candidate, sdp }) => {
            if (candidate) {
                await peerConnection.addIceCandidate(new RTCIceCandidate(candidate));
            }
            if (sdp) {
                if (sdp.type === "offer") {
                    await peerConnection.setRemoteDescription(new RTCSessionDescription(sdp));
                    const answer = await peerConnection.createAnswer();
                    await peerConnection.setLocalDescription(answer);
                    socket.emit("signal", { room, sdp: answer });
                } else if (sdp.type === "answer") {
                    await peerConnection.setRemoteDescription(new RTCSessionDescription(sdp));
                }
            }
        });

        // Nếu là người tạo kết nối, gửi offer
        setTimeout(async () => {
            const offer = await peerConnection.createOffer();
            await peerConnection.setLocalDescription(offer);
            socket.emit("signal", { room, sdp: offer });
        }, 1000);
    })
    .catch(console.error);
