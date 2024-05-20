using Microsoft.AspNetCore.Mvc;
using Newtonsoft.Json;

namespace OutlookEmailService.Controllers
{
    [ApiController]
    [Route("api/[controller]")]
    public class EmailController : ControllerBase
    {
        private readonly IEmailService _emailService;

        public EmailController(IEmailService emailService)
        {
            _emailService = emailService;
        }

        [HttpPost("send")]
        public async Task<IActionResult> SendEmail([FromBody] MessageInfo messageInfo)
        {
            var messageParams = JsonConvert.SerializeObject(messageInfo);
            var result = await _emailService.SendEmailAsync(messageParams);
            return Ok(result);
        }
    }
}
