using Microsoft.Exchange.WebServices.Data;
using Newtonsoft.Json;
using System.Net;

namespace OutlookEmailService
{
    public interface IEmailService
    {
        Task<string> SendEmailAsync(string messageParams);
    }

    public class EmailService : IEmailService
    {
        private readonly string _login;
        private readonly string _password;
        private readonly string _exchangeServer;

        public EmailService(IConfiguration configuration)
        {
            _login = configuration["EmailSettings:Login"];
            _password = configuration["EmailSettings:Password"];
            _exchangeServer = configuration["EmailSettings:ExchangeServer"];
        }

        public async Task<string> SendEmailAsync(string messageParams)
        {
            var service = new ExchangeService(ExchangeVersion.Exchange2013_SP1)
            {
                Credentials = new NetworkCredential(_login, _password),
                Url = new Uri(_exchangeServer)
            };

            var messageInfo = JsonConvert.DeserializeObject<MessageInfo>(messageParams);
            var emailMessage = new EmailMessage(service)
            {
                Subject = messageInfo.Subject,
                Body = new MessageBody(messageInfo.BodyType.ToLower() == "html" ? BodyType.HTML : BodyType.Text, messageInfo.Body)
            };

            foreach (var recipient in messageInfo.Rerecipients)
            {
                emailMessage.ToRecipients.Add(recipient.Email);
            }

            emailMessage.SendAndSaveCopy();
            return "Email sent successfully";
        }
    }
}
