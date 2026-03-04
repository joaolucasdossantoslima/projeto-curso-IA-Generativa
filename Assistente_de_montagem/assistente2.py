import React, { useState, useEffect, useRef } from 'react';
import { Send, Phone, Video, MoreVertical, CheckCheck, ArrowLeft, Cpu } from 'lucide-react';

const App = () => {
  const [messages, setMessages] = useState([
    {
      id: 1,
      text: "Olá! Bom dia! Eu sou o Zar, seu assistente inteligente. Hoje vou te ajudar na escolha das suas peças. 🖥️\n\nO que está procurando?\n\n1️⃣ - Peças específicas\n2️⃣ - Montar um computador do Zero\n3️⃣ - Dúvidas",
      sender: 'zar',
      time: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
      status: 'read'
    }
  ]);
  const [inputValue, setInputValue] = useState('');
  const [isTyping, setIsTyping] = useState(false);
  const [step, setStep] = useState('menu'); 
  const [tempData, setTempData] = useState({ retryCount: 0 });
  const messagesEndRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages, isTyping]);

  const addMessage = (text, sender) => {
    const newMessage = {
      id: Date.now(),
      text,
      sender,
      time: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
      status: sender === 'user' ? 'sent' : 'read'
    };
    setMessages(prev => [...prev, newMessage]);
    return newMessage;
  };

  const handleSend = (e) => {
    e.preventDefault();
    if (!inputValue.trim()) return;

    const userText = inputValue.trim();
    addMessage(userText, 'user');
    setInputValue('');
    processZarResponse(userText);
  };

  const getRecommendations = (part, isRetry) => {
    const p = part.toLowerCase();
    if (p.includes('ram')) {
      return isRetry ? 
        `🟢 **Nível 1 (Entrada)**\nMemória ADATA Premier 8GB 3200MHz DDR4\n💰 ~R$ 170,00\n\n` +
        `🔵 **Nível 2 (Intermediário)**\nMemória Team Group T-Force 16GB (2x8) 3200MHz RGB\n💰 ~R$ 380,00\n\n` +
        `🟣 **Nível 3 (High-End)**\nMemória G.Skill Trident Z Neo 32GB (2x16) 3600MHz CL16\n💰 ~R$ 1.100,00` :
        `🟢 **Nível 1 (Entrada)**\nMemória Crucial Basics 8GB 3200MHz DDR4 CL22\n💰 ~R$ 185,00\n\n` +
        `🔵 **Nível 2 (Intermediário)**\nMemória Kingston Fury Beast 16GB (2x8) 3600MHz CL16\n💰 ~R$ 430,00\n\n` +
        `🟣 **Nível 3 (High-End)**\nMemória Corsair Vengeance RGB Pro 32GB (2x16) 4000MHz\n💰 ~R$ 915,00`;
    } else if (p.includes('vídeo') || p.includes('video') || p.includes('gpu')) {
      return isRetry ?
        `🟢 **Nível 1 (Entrada)**\nPlaca de Vídeo ASUS NVIDIA GeForce GTX 1650 4GB\n💰 ~R$ 980,00\n\n` +
        `🔵 **Nível 2 (Intermediário)**\nPlaca de Vídeo AMD Radeon RX 7600 8GB Sapphire Pulse\n💰 ~R$ 1.850,00\n\n` +
        `🟣 **Nível 3 (High-End)**\nPlaca de Vídeo NVIDIA GeForce RTX 4070 Super 12GB MSI Slim\n💰 ~R$ 4.500,00` :
        `🟢 **Nível 1 (Entrada)**\nPlaca de Vídeo PowerColor AMD Radeon RX 6600 8GB\n💰 ~R$ 1.340,00\n\n` +
        `🔵 **Nível 2 (Intermediário)**\nPlaca de Vídeo NVIDIA GeForce RTX 4060 Ti 8GB Galax\n💰 ~R$ 2.640,00\n\n` +
        `🟣 **Nível 3 (High-End)**\nPlaca de Vídeo NVIDIA GeForce RTX 4080 Super 16GB ASUS ROG Strix\n💰 ~R$ 8.900,00`;
    } else {
      return isRetry ?
        `🟢 **Nível 1 (Entrada)**\nOpção Econômica (Marca Lexar/Netac)\n💰 ~R$ 150,00\n\n` +
        `🔵 **Nível 2 (Intermediário)**\nOpção Estável (Marca Gigabyte/MSI)\n💰 ~R$ 500,00\n\n` +
        `🟣 **Nível 3 (High-End)**\nOpção Elite (Marca EVGA/Zotac)\n💰 ~R$ 1.000,00` :
        `🟢 **Nível 1 (Entrada)**\nOpção Standard (Marca Kingston/Crucial)\n💰 ~R$ 250,00\n\n` +
        `🔵 **Nível 2 (Intermediário)**\nOpção Performance (Marca Corsair/Asus)\n💰 ~R$ 600,00\n\n` +
        `🟣 **Nível 3 (High-End)**\nOpção Premium (Marca ROG/Aorus)\n💰 ~R$ 1.200,00+`;
    }
  };

  const processZarResponse = (text) => {
    setIsTyping(true);
    const lowerText = text.toLowerCase().trim();
    
    setTimeout(() => {
      setIsTyping(false);
      
      switch(step) {
        case 'menu':
          if (text === '1') {
            addMessage("1️⃣ Certo, me diga qual componente seria? (Ex: memória RAM, SSD, placa de vídeo, etc)", 'zar');
            setStep('specific_part');
          } else if (text === '2') {
            addMessage("2️⃣ Entendido! Vamos montar uma máquina do zero. Primeiro, qual será o perfil de uso?\n\n1- Trabalho/Estudo\n2- Jogos\n3- Híbrido", 'zar');
            setStep('build_zero_profile');
          } else if (text === '3') {
            addMessage("3️⃣ Entendi. Qual sua dúvida técnica?\n\n- O que é Gargalo?\n- DDR4 vs DDR5?\n- Compatibilidade de Processador?", 'zar');
            setStep('doubts');
          } else {
            addMessage("Ops! ❌ Por favor, digite apenas o número da opção (1, 2 ou 3).", 'zar');
          }
          break;

        case 'specific_part':
          setTempData({ ...tempData, part: text, retryCount: 0 });
          addMessage(`Ok, você quer ver sobre ${text}. Para eu ser assertivo, me informe o modelo da sua placa mãe:`, 'zar');
          setStep('motherboard');
          break;

        case 'motherboard':
          setTempData({ ...tempData, mb: text });
          addMessage(`Placa ${text} identificada. Qual tipo de uso?\n\n1- Trabalho/Estudo\n2- Jogos\n3- Híbrido`, 'zar');
          setStep('specific_usage');
          break;

        case 'specific_usage':
          addMessage("Consultando opções disponíveis... 🔍", 'zar');
          setTimeout(() => {
            let rec = `Aqui estão as melhores opções de **${tempData.part}**:\n\n` + getRecommendations(tempData.part, false);
            rec += `\n\nVocê está satisfeito com essas opções? Sim ou Não`;
            addMessage(rec, 'zar');
            setStep('satisfaction_check');
          }, 1000);
          break;

        case 'build_zero_profile':
          addMessage("Excelente escolha. Analisei 3 configurações completas:\n\n" +
            "💰 **Nível 1:** ~R$ 2.500\n" +
            "💰 **Nível 2:** ~R$ 5.500\n" +
            "💰 **Nível 3:** ~R$ 12.000+\n\n" +
            "Qual faixa você gostaria de ver o detalhamento? (Digite 1, 2 ou 3)", 'zar');
          setStep('build_zero_details');
          break;

        case 'build_zero_details':
          addMessage(`Compilando lista de componentes do Nível ${text}... 📑`, 'zar');
          setTimeout(() => {
            let details = "";
            if (text === '1') details = "💻 **Nível 1**\n- CPU: i3-12100\n- MB: H610M\n- RAM: 8GB Crucial\n- Total: R$ 1.800";
            else if (text === '2') details = "🎮 **Nível 2**\n- CPU: R5 5600\n- MB: B550M Aorus\n- GPU: RTX 4060\n- Total: R$ 4.885";
            else details = "🔥 **Nível 3**\n- CPU: i9-14900K\n- GPU: RTX 4090\n- Total: R$ 25.980";
            
            addMessage(`${details}\n\nVocê está satisfeito com essas opções? Sim ou Não`, 'zar');
            setStep('satisfaction_check');
          }, 1000);
          break;

        case 'doubts':
          addMessage("O 'Gargalo' ocorre quando um componente limita o outro. O ideal é ter CPU e GPU equilibrados. 🧠\n\nDigite **Menu** para voltar ou selecione outra dúvida.", 'zar');
          setStep('final');
          break;

        case 'satisfaction_check':
          const isPositive = lowerText === 'sim' || lowerText === 's' || lowerText.includes("satisfeito");
          const isNegative = lowerText === 'não' || lowerText === 'nao' || lowerText === 'n' || lowerText.includes("não satisfeito");

          if (isPositive) {
            addMessage("Obrigada, fico feliz em ajudar. Estou sempre a disposição. 😊", 'zar');
            setTimeout(() => {
              addMessage("Atendimento finalizado. Se precisar iniciar uma nova conversa, basta digitar **Menu** ou **Oi**.", 'zar');
              setStep('final');
            }, 1000);
          } else if (isNegative) {
            if (tempData.retryCount === 0) {
              addMessage("Poxa! Quer que eu gere outras opções ou deseja sair? (Responda: Outras opções ou Sair)", 'zar');
              setStep('retry_options');
            } else {
              addMessage("Sinto muito não ter conseguido satisfazê-lo com essas opções. 😔", 'zar');
              setTimeout(() => {
                addMessage("Deseja selecionar outra peça ou voltar ao menu inicial? (Responda: Outra peça ou Menu)", 'zar');
                setStep('failed_options_choice');
              }, 1000);
            }
          } else {
            addMessage("Por favor, responda com **Sim** ou **Não**.", 'zar');
          }
          break;

        case 'retry_options':
          if (lowerText.includes("outra") || lowerText.includes("opções")) {
            addMessage("Certo! Buscando modelos diferentes no estoque... 🔄", 'zar');
            setTempData({ ...tempData, retryCount: 1 });
            setTimeout(() => {
              let rec = `Aqui estão novas opções para **${tempData.part}**:\n\n` + getRecommendations(tempData.part, true);
              rec += `\n\nVocê está satisfeito com essas opções? Sim ou Não`;
              addMessage(rec, 'zar');
              setStep('satisfaction_check');
            }, 1200);
          } else {
            addMessage("Entendido. Se precisar, digite **Menu**! 👋", 'zar');
            setStep('final');
          }
          break;

        case 'failed_options_choice':
          if (lowerText.includes("peça") || lowerText.includes("peca")) {
            addMessage("Com certeza! Qual componente você quer ver agora? (Ex: Processador, Gabinete, Fonte...)", 'zar');
            setStep('specific_part');
          } else {
            addMessage("Voltando ao menu principal... \n\n1️⃣ - Peças específicas\n2️⃣ - Montar um computador do Zero\n3️⃣ - Dúvidas", 'zar');
            setStep('menu');
          }
          break;

        case 'final':
          if (lowerText === 'menu' || lowerText === 'oi') {
            addMessage("Olá! Como posso te ajudar? \n\n1️⃣ - Peças específicas\n2️⃣ - Montar um computador do Zero\n3️⃣ - Dúvidas", 'zar');
            setStep('menu');
          } else {
            addMessage("Para iniciar uma nova conversa, digite **Menu** ou **Oi**.", 'zar');
          }
          break;

        default:
          setStep('menu');
          break;
      }
    }, 800);
  };

  return (
    <div className="flex items-center justify-center min-h-screen bg-slate-900 p-0 sm:p-4 font-sans">
      <div className="w-full max-w-[450px] h-[100vh] sm:h-[800px] bg-[#E5DDD5] flex flex-col shadow-2xl relative overflow-hidden sm:rounded-[30px] border-[6px] border-slate-800">
        
        {/* Header WhatsApp */}
        <div className="bg-[#075E54] text-white p-4 flex items-center justify-between shadow-md pt-10 sm:pt-6">
          <div className="flex items-center gap-3">
            <ArrowLeft size={20} className="cursor-pointer" />
            <div className="w-10 h-10 bg-white rounded-full flex items-center justify-center text-[#075E54]">
              <Cpu size={24} />
            </div>
            <div>
              <h2 className="font-bold text-sm leading-tight">Zar - Assistente</h2>
              <p className="text-[10px] opacity-80">online</p>
            </div>
          </div>
          <div className="flex items-center gap-4 opacity-90">
            <Video size={20} />
            <Phone size={18} />
            <MoreVertical size={20} />
          </div>
        </div>

        {/* Chat Body */}
        <div 
          className="flex-1 overflow-y-auto p-4 space-y-3 bg-repeat" 
          style={{ backgroundImage: `url('https://user-images.githubusercontent.com/15075759/28719144-86dc0f70-73b1-11e7-911d-60d70fcded21.png')`, backgroundSize: '400px' }}
        >
          {messages.map((msg) => (
            <div key={msg.id} className={`flex ${msg.sender === 'user' ? 'justify-end' : 'justify-start'}`}>
              <div className={`max-w-[85%] p-3 rounded-xl shadow-sm relative ${
                  msg.sender === 'user' ? 'bg-[#DCF8C6] rounded-tr-none' : 'bg-white rounded-tl-none'
                }`}>
                <div className="whitespace-pre-wrap text-[13px] leading-relaxed text-slate-800">
                  {msg.text}
                </div>
                <div className="flex items-center justify-end gap-1 mt-1">
                  <span className="text-[9px] text-slate-400 uppercase">{msg.time}</span>
                  {msg.sender === 'user' && <CheckCheck size={14} className="text-sky-500" />}
                </div>
              </div>
            </div>
          ))}
          {isTyping && (
            <div className="flex justify-start">
              <div className="bg-white p-3 rounded-xl rounded-tl-none shadow-sm flex gap-1">
                <span className="w-1.5 h-1.5 bg-slate-400 rounded-full animate-bounce"></span>
                <span className="w-1.5 h-1.5 bg-slate-400 rounded-full animate-bounce [animation-delay:0.2s]"></span>
                <span className="w-1.5 h-1.5 bg-slate-400 rounded-full animate-bounce [animation-delay:0.4s]"></span>
              </div>
            </div>
          )}
          <div ref={messagesEndRef} />
        </div>

        {/* Input */}
        <form onSubmit={handleSend} className="p-3 bg-[#F0F2F5] flex items-center gap-2">
          <div className="flex-1 bg-white rounded-full px-4 py-2.5 flex items-center shadow-sm">
            <input 
              type="text" 
              placeholder="Digite aqui..."
              className="flex-1 outline-none text-sm bg-transparent"
              value={inputValue}
              onChange={(e) => setInputValue(e.target.value)}
            />
          </div>
          <button 
            type="submit"
            className="w-12 h-12 bg-[#00A884] text-white rounded-full flex items-center justify-center shadow-md active:scale-90 transition-all"
          >
            <Send size={20} className="ml-1" />
          </button>
        </form>
      </div>
    </div>
  );
};

export default App;
