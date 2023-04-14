import {
  Controller,
  Post,
  Query,
  UploadedFile,
  UseGuards,
  UseInterceptors,
} from '@nestjs/common'
import {
  ApiBearerAuth,
  ApiBody,
  ApiConsumes,
  ApiOperation,
  ApiTags,
} from '@nestjs/swagger'
import { FileInterceptor } from '@nestjs/platform-express'
import { multerOptions } from '../common/utils/multer.options'
import { JwtAuthGuard } from '../auth/jwt/jwt-auth.guard'
import { User } from '../common/decorators/user.decorator'
import { UserEntity } from '../auth/entities/user.entity'
import { AuthService } from '../auth/auth.service'
import { ItemService } from '../item/item.service'

@Controller('upload')
@ApiTags('upload')
export class UploadController {
  constructor(
    private readonly authService: AuthService,
    private readonly itemService: ItemService,
  ) {}

  @UseGuards(JwtAuthGuard)
  @Post('avatar')
  @UseInterceptors(FileInterceptor('image', multerOptions('images')))
  @ApiBearerAuth('access-token')
  @ApiConsumes('multipart/form-data')
  @ApiOperation({
    summary: 'To upload a single avatar image file',
  })
  @ApiBody({
    schema: {
      type: 'object',
      properties: {
        image: {
          type: 'string',
          format: 'binary',
        },
      },
    },
  })
  async uploadAvatarImage(
    @User() user: UserEntity,
    @UploadedFile() image: Express.Multer.File,
  ) {
    const path = `http://localhost:${process.env.PORT}/media/images/${image.filename}`
    return await this.authService.avatarImageUpload(user.pk, path)
  }

  @UseGuards(JwtAuthGuard)
  @Post('item')
  @UseInterceptors(FileInterceptor('image', multerOptions('images')))
  @ApiBearerAuth('access-token')
  @ApiConsumes('multipart/form-data')
  @ApiOperation({
    summary: 'To upload a single item image file',
  })
  @ApiBody({
    schema: {
      type: 'object',
      properties: {
        image: {
          type: 'string',
          format: 'binary',
        },
      },
    },
  })
  async uploadItemCoverImage(
    @User() user: UserEntity,
    @UploadedFile() image: Express.Multer.File,
    @Query('pk') pk: number,
  ) {
    const path = `http://localhost:${process.env.PORT}/media/images/${image.filename}`
    return await this.itemService.uploadItemCoverImage(user, pk, path)
  }
}
