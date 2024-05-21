function validarSenha(event) {
    var senha = document.getElementById('senha').value;
    var mensagem = '';

    if (senha.length < 8) {
        mensagem += 'A senha deve ter pelo menos 8 caracteres. \n';
    }
    if (!/[A-Z]/.test(senha)) {
        mensagem += 'A senha deve ter pelo menos uma letra maiúscula. \n';
    }
    if (!/[a-z]/.test(senha)) {
        mensagem += 'A senha deve ter pelo menos uma letra minúscula. \n';
    }

    if (mensagem !== '') {
        document.getElementById('mensagem').innerText = mensagem;
        event.preventDefault();
        return false;
    }

    document.getElementById('mensagem').innerText = '';
    return true;
}

function formatCPF(input) {
    input.value = input.value.replace(/\D/g, '');
    if (input.value.length > 3) {
        input.value = input.value.slice(0, 3) + '.' + input.value.slice(3);
    }
    if (input.value.length > 7) {
        input.value = input.value.slice(0, 7) + '.' + input.value.slice(7);
    }
    if (input.value.length > 11) {
        input.value = input.value.slice(0, 11) + '-' + input.value.slice(11);
    }
}

function formatTelefone(input) {
    input.value = input.value.replace(/\D/g, '');

    if (input.value.length > 2) {
        input.value = '(' + input.value.slice(0, 2) + ')' + input.value.slice(2);
    }

    if (input.value.length > 9) {
        input.value = input.value.slice(0, 9) + '-' + input.value.slice(9);
    }
  }

  function formatCEP(input) {
      input.value = input.value.replace(/\D/g, '');
      if (input.value.length > 5) {
          input.value = input.value.slice(0, 5) + '-' + input.value.slice(5);
      }
  }

  function allowOnlyNumbers(input) {
      input.value = input.value.replace(/\D/g, '');
  }

  function formatDate(input) {
      input.value = input.value.replace(/[^\d/]/g, '');
      if (input.value.length > 2 && input.value.charAt(2) !== '/') {
          input.value = input.value.slice(0, 2) + '/' + input.value.slice(2);
      }
      if (input.value.length > 5 && input.value.charAt(5) !== '/') {
          input.value = input.value.slice(0, 5) + '/' + input.value.slice(5);
      }
  }

  document.querySelector('select[name="sexo"]').addEventListener('change', function () {
      var gestanteContainer = document.getElementById('gestante-container');
      if (this.value === 'feminino') {
        gestanteContainer.style.display = 'block';
      } else {
        gestanteContainer.style.display = 'none';
      }
  });

  function handleFormSubmission(event) {
    event.preventDefault();
    
    if (!validarSenha(event)) {
        return;
    }
    
    fetch('/register', {
        method: 'POST',
        body: new FormData(event.target) 
    })
    .then(response => response.json())
    .then(data => {
        if (data.error) {
            document.getElementById('mensagem').innerText = data.error; 
        } 
    })
    .catch(error => console.error('Error:', error));
}
